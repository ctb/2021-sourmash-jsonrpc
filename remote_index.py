from jsonrpcclient import request
import sourmash
from sourmash.index import Index, IndexSearchResult
from sourmash import search


class RemoteIndex(Index):
    is_database = True
    def __init__(self, url, database_id=0):
        self.url = url
        self.database_id = database_id

    def __bool__(self):
        return True

    def __len__(self):
        response = request(self.url, "len", database_id=self.database_id)
        return response.data.result

    def check_is_sourmash(self):
        response = request(self.url, "check_is_sourmash")
        return response.data.result

    def signatures(self):
        raise NotImplementedError

    def signatures_with_location(self):
        raise NotImplementedError

    def insert(self, *args):
        raise NotImplementedError

    def save(self, *args):
        raise NotImplementedError

    def load(self, *args):
        raise NotImplementedError

    def find(self, search_fn, query, **kwargs):
        database_id = self.database_id
        search_type = int(search_fn.search_type)
        threshold = search_fn.threshold
        best_only = False
        if isinstance(search_fn, search.JaccardSearchBestOnly):
            best_only = True

        query_json = sourmash.save_signatures([query])
        query_json = query_json.decode('utf-8')

        response = request(self.url, "find",
                           database_id=database_id,
                           search_type=search_type,
                           threshold=threshold,
                           best_only=best_only,
                           query_ss_json = query_json)

        results = []
        for (score, r_json, loc) in response.data.result:
            result_ss = sourmash.load_one_signature(r_json)
            sr = IndexSearchResult(score, result_ss, loc)
            results.append(sr)

        return results

    def select(self, **kwargs):
        if 'picklist' in kwargs:
            assert not kwargs.get('picklist'), "we do not support picklists for remote index yet"
            del kwargs['picklist']

        response = request(self.url, "select", **kwargs)

        database_id = response.data.result
        #print(f'got database_id={database_id}')
        return RemoteIndex(self.url, database_id)
