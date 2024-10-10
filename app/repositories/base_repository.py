

class BaseRepository:
    def __init__(self, db, model) -> None:
        self.db = db
        self.model = model


    def find_by_id(self, id: int):
        return self.db.query(self.model).filter(self.model.id == id).first()

    def create(self, data):
        instance = self.model(**data)
        self.db.add(instance)
        self.db.commit()
        self.db.refresh(instance)
        return instance

    def create_from_instance(self, instance):
        self.db.add(instance)
        self.db.commit()
        self.db.refresh(instance)
        return instance

    def create_without_return(self, data):
        instance = self.model(**data)
        self.db.add(instance)
        self.db.commit()

    def bulk_create(self, data):
        instances = [self.model(**item) for item in data]
        for instance in instances:
            self.db.add(instance)
        self.db.commit()
        for instance in instances:
            self.db.refresh(instance)
        return instances

    def delete_by_id(self, id):
        number = self.db.query(self.model).filter(self.model.id == id).delete()
        self.db.commit()
        return number

    def update(self, instance):
        self.db.add(instance)
        self.db.commit()
        self.db.refresh(instance)
        return instance
