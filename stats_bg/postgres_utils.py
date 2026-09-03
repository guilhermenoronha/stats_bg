from sqlalchemy import create_engine, text
import pandas as pd
import stats_bg.board_games as bg
import logging
from pandas import DataFrame


class PostgresUtils:
    """Utility class for PostgreSQL table reads and writes.

    The class owns a SQLAlchemy engine created from the connection string and
    reuses it across read, save, and truncate operations.

    Args:
        sql_string (str): PostgreSQL connection string used to create the engine.
    """
    
    def __init__(self, sql_string: str):
        self.sql_string = sql_string
        self.engine = create_engine(sql_string)
        self.engine.execution_options(autocommit=True)        

    def get_games_data(
        self, db: str, schema: str, columns: list[str]
    ) -> DataFrame:
        """Get distinct data from the GAMES table.

        If the table cannot be read, the method bootstraps it from Ludopedia
        data using the PLAYERS table, then reads it again.

        Args:
            db (str): database name
            schema (str): schema name
            columns (list[str]): columns to retrieve

        Returns:
            DataFrame: table
        """
        columns = ", ".join(f'"{column}"' for column in columns)
        qry = f'SELECT DISTINCT {columns} FROM {db}.{schema}."GAMES"'
        with self.engine.begin() as conn:
            try:
                return pd.read_sql(qry, conn)
            except:
                try:
                    bgs
                except:
                    players = self.get_table_data(
                        db, schema, "PLAYERS", ["ID", "LUDOPEDIA_NICKNAME"]
                    )
                    bgs = bg.get_all_bgs(players)
                    self.save_table(
                        bg.create_board_games_table(bgs), schema, "GAMES"
                    )
                    return pd.read_sql(qry, conn)


    def get_table_data(
        self, db: str, schema: str, table: str, columns: list[str] = None
    ) -> DataFrame:
        """Get data from a database table.

        Args:
            db (str): database name
            schema (str): schema name
            table (str): table name
            columns (list[str]): columns to retrieve

        Returns:
            DataFrame: table

        Raises:
            RuntimeError: if the table cannot be read.
        """
        if columns:
            columns = ", ".join(f'"{column}"' for column in columns)
        else:
            columns = "*"
        qry = f'SELECT {columns} FROM {db}.{schema}."{table}"'
        with self.engine.begin() as conn:
            try:
                return pd.read_sql(qry, conn)
            except Exception as exc:
                raise RuntimeError(
                    f'Failed to read table {db}.{schema}."{table}" with query: {qry}'
                ) from exc


    def save_table(
        self, df: DataFrame, schema: str, table_name: str, mode="replace"
    ) -> None:
        """Save a DataFrame into a database table.

        In replace mode, the method truncates the table before appending the new
        DataFrame. This avoids cascade drops in the database.

        Args:
            df (DataFrame): table to be saved
            schema (str): name of the schema on database
            table_name (str): name of the table to save the df
            mode (str, optional): accept values replace or append. Defaults to 'replace'.

        Raises:
            ValueError: if mode is not 'append' or 'replace'.
        """
        if mode.lower() not in ("append", "replace"):
            raise ValueError("Mode must be 'append' or 'replace'!")
        if mode == "replace":
            self.truncate_table(schema, table_name)
        with self.engine.begin() as conn:
            df.to_sql(name=table_name, con=conn, if_exists="append", schema=schema, index=False)
            if mode.lower() == "replace":
                logging.info(
                    f"Table {table_name} was successfully created with {len(df)} rows."
                )
            else:
                logging.info(f"{len(df)} rows were added to {table_name} table.")


    def truncate_table(self, schema: str, table_name: str) -> None:
        """Truncate a table before appending new data.

        Args:
            schema (str): schema name
            table_name (str): table name
        """
        try:
            with self.engine.begin() as conn:
                conn.execute(text(f'TRUNCATE TABLE {schema}."{table_name}"'))
                conn.commit()
        except:
            logging.warning(
                f"Table {table_name} wasn't truncated because it doesn't exist."
            )

    def delete_table_data(self, db: str, schema: str, table_name: str, where_condition: str):
        """Delete data according to condition specified. Use it with caution.

        Args:
            db (str): database name
            schema (str): schema name
            table_name (str): table name
            where_condition (str): filter condition to select rows to be deleted. E.g: game_name = 'XYZ'       
        """
        with self.engine.begin() as conn:
            delete_str = f'DELETE FROM  {db}.{schema}."{table_name}" WHERE {where_condition}'
            logging.warning(f"Deleting data with the following query: {delete_str}")
            result = conn.execute(text(delete_str))
            conn.commit()
            logging.info(f"Query deleted {result.rowcount} rows successfully.")