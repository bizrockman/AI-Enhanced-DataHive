from models import DataHiveBaseModel, Media, GithubProject

class BaseDAO:
    def create(self, entity):
        raise NotImplementedError

    def read(self, id):
        raise NotImplementedError

    def update(self, id, entity):
        raise NotImplementedError

    def delete(self, id):
        raise NotImplementedError

    def save(self, base_model: DataHiveBaseModel):
        #TODO Intermediate solution try later to consolidate everythin into one method
        if isinstance(base_model, Media):
            return self._save_media(base_model)
        if isinstance(base_model, GithubProject):
            return self._save_github_projects(base_model)
        else:
            raise ValueError("Unsupported model type")

    def _save_media(self, media: Media):
        # TODO Intermediate solution try later to consolidate everythin into one method
        raise NotImplementedError

    def _save_github_projects(self, github_project: GithubProject):
        # TODO Intermediate solution try later to consolidate everythin into one method
        raise NotImplementedError

    def get_latest_data_date(self, creator_name: str, content_type: str):
        raise NotImplementedError


    # Füge hier weitere methodenspezifische Operationen hinzu
