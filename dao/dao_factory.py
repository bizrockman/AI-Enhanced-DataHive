import os

from dao import BaseDAO, SupabaseDAO


def dao_factory() -> BaseDAO:
    dao_impl = os.getenv('DAO_IMPL', 'supabase')
    if dao_impl == 'supabase':
        return SupabaseDAO()
    else:
        return SupabaseDAO()