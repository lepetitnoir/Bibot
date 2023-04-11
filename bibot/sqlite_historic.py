from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, Float, String, select, BigInteger
from sqlalchemy.orm import declarative_base, Session

# TODO maybe add symbol and/or timestamp to db file name and handle the creation of the out folder
engine = create_engine("sqlite:///../out/binance_historic_trades.db", echo=False, future=True)
base = declarative_base()


class HistoricTrade(base):
    __tablename__ = "historic_trades"

    tradeId = Column(Integer, primary_key=True)
    symbol = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    quantity = Column(Float, nullable=False)
    timestamp = Column(BigInteger, nullable=False)

    def __repr__(self):
        return f"historic_trade(tradeId={self.tradeId!r}, symbol={self.symbol!r}, price={self.price!r}, " \
               f"quantity={self.quantity!r}, timestamp={self.timestamp!r})"


# TODO doesn't recreate the db if schema changes and the file exists, needs handling
def setup_sql_tables():
    base.metadata.create_all(engine)


def create_historic_trade(trade, symbol):
    return HistoricTrade(tradeId=trade.get("a"), symbol=symbol, price=trade.get("p"), quantity=trade.get("q"),
                         timestamp=trade.get("T"))


# TODO beware returns the complete table and might take a while
def select_all_data():
    result = []
    with Session(engine) as session:
        statement = select(HistoricTrade)
        for data in session.scalars(statement):
            result.append(data)

        return result


def insert_data(historic_trades, symbol):
    """
    Inserts data by batch into a sqlite db.
    :param historic_trades: array of dict entries representing an aggregated trade.
    :param symbol: the symbol the trade belongs to. E.g. "EURBTC"
    """
    trades = list(map(lambda trade: create_historic_trade(trade, symbol), historic_trades))

    with Session(engine) as session:
        session.bulk_save_objects(trades)
        session.commit()
