import os
from datetime import datetime, timedelta

from dao import BaseDAO
from models import Media, GithubProject
from supabase import create_client, Client


class SupabaseDAO(BaseDAO):

    def __init__(self):
        supabase_url = os.getenv('SUPABASE_URL')
        supabase_api_key = os.getenv('SUPABASE_KEY')

        self.supabase_client: Client = create_client(supabase_url, supabase_api_key)

    def create(self, entity):
        # Implementiere die Methode unter Verwendung von Supabase
        pass

    def read(self, id):
        # Implementiere die Methode unter Verwendung von Supabase
        pass

    def update(self, entity):

        pass

    def _save_github_projects(self, github_project: GithubProject):
        project_data = github_project.dict()

        if project_data['url'] is not None:
            project_data['url'] = str(project_data['url'])

        if isinstance(project_data['created_at'], datetime):
            project_data['created_at'] = project_data['created_at'].isoformat()
        if isinstance(project_data['updated_at'], datetime):
            project_data['updated_at'] = project_data['updated_at'].isoformat()

        # Entferne Schlüssel mit None-Werten, wenn diese nicht in der Datenbank gespeichert werden sollen
        project_data = {k: v for k, v in project_data.items() if v is not None}

        result = self.supabase_client.table('t_github_projects').insert(project_data).execute()

        return result

    def _save_media(self, media: Media):
        media_data = media.dict()

        if media_data['media_url'] is not None:
            media_data['media_url'] = str(media_data['media_url'])
        if media_data['reference_url'] is not None:
            media_data['reference_url'] = str(media_data['reference_url'])

        if isinstance(media_data['media_created_at'], datetime):
            media_data['media_created_at'] = media_data['media_created_at'].isoformat()
        if isinstance(media_data['created_at'], datetime):
            media_data['created_at'] = media_data['created_at'].isoformat()
        if isinstance(media_data['updated_at'], datetime):
            media_data['updated_at'] = media_data['updated_at'].isoformat()

        # Entferne Schlüssel mit None-Werten, wenn diese nicht in der Datenbank gespeichert werden sollen
        media_data = {k: v for k, v in media_data.items() if v is not None}

        result = self.supabase_client.table('t_media').insert(media_data).execute()

        return result

    def get_latest_data_date(self, creator_name: str, table_name: str):
        # Get date from the latest message to the telegram table - using topic / reporter
        #table_name = f't_{content_type}'
        result = self.supabase_client.table(table_name) \
            .select('created_at') \
            .eq('creator', creator_name) \
            .order('created_at', desc=True) \
            .limit(1) \
            .execute()

        if result.data:
            # Gehe davon aus, dass `created_at` das Datum beinhaltet
            return datetime.fromisoformat(result.data[0]['created_at'])
        else:
            return datetime.now() - timedelta(weeks=1)

    # Implementiere die restlichen Methoden entsprechend
