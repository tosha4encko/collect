from core.data_models import MarketTypes, Meta

EXCHANGE = 'ByBit'

meta_opt: dict[MarketTypes, Meta] = {
    MarketTypes.SPOT: Meta(exchange=EXCHANGE, market_type=MarketTypes.SPOT),
    MarketTypes.LINEAR: Meta(exchange=EXCHANGE, market_type=MarketTypes.LINEAR),
    MarketTypes.INVERSE: Meta(exchange=EXCHANGE, market_type=MarketTypes.INVERSE),
    MarketTypes.OPTION: Meta(exchange=EXCHANGE, market_type=MarketTypes.OPTION),
}