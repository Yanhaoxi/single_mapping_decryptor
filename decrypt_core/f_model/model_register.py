class Model_Registry:
    def __init__(self):
        self.models = {}

    def register(self, name, cls):
        self.models[name] = cls

    def get_model(self, name):
        try:
            return self.models.get(name)
        except KeyError:
            raise KeyError(f"Model {name} not found in registry")

    def list_models(self):
        return list(self.models.keys())

model_registry = Model_Registry()
