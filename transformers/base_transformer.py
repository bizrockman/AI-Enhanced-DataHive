import os
from typing import Union, Collection

from string import Template
from utils.text_helper import escape_html

from transformers.models import Content


class BaseTransformer:
    def __init__(self, creator_name, template_file_name, language):
        from dao.dao_factory import dao_factory
        self.dao = dao_factory()
        self.language = language
        self.creator_name = creator_name
        self.template_path = os.path.join(os.path.dirname(__file__), 'templates', template_file_name)

    def save(self, content: Union[Content, Collection[Content]]):
        if isinstance(content, Collection):
            results = [self.dao.create(c) for c in content]
            return results
        else:
            result = self.dao.create(content)
            return result

    def create_content(self, template_data):
        template_data = {k: escape_html(v) for k, v in template_data.items()}

        with open(self.template_path, 'r', encoding='utf-8') as file:
            template_content = file.read()

        template = Template(template_content)
        return template.safe_substitute(template_data)
