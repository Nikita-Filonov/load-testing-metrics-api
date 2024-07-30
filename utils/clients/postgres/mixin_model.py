from utils.clients.postgres.create_model import CreateModel
from utils.clients.postgres.filter_model import FilterModel


class MixinModel(
    FilterModel,
    CreateModel,
):
    __abstract__ = True
