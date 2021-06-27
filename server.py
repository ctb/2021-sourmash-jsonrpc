from jsonrpcserver import method, serve
import sourmash
from sourmash.search import JaccardSearch, JaccardSearchBestOnly

LIMIT=50

class ServedIndex:
    def __init__(self, db):
        self.db = db
        self._serving_dbs = {}
        self._serve_index = 1

    def _get_database(self, database_id):
        if database_id == 0:
            db = self.db
        else:
            db = self._serving_dbs[database_id]
        return db

    def len(self, database_id=0):
        db = self._get_database(database_id)
        return len(db)

    def select(self, *, ksize=None):
        "select on a DB, return the index of the new db"
        new_db = self.db.select(ksize=ksize)
        self._serve_index += 1
        cur_idx = self._serve_index
        self._serving_dbs[cur_idx] = new_db
        print(f'built new idx', cur_idx)
        return cur_idx

    def find(self, database_id=0, search_type=None,
             best_only=False, threshold=0, query_ss_json=None):
        db = self._get_database(database_id)

        if best_only:
            cls = JaccardSearchBestOnly
        else:
            cls = JaccardSearch

        print(f'constructing search_fn with {search_type}, {best_only}, {threshold}')
        search_fn = cls(search_type, threshold=threshold)

        assert query_ss_json
        query = sourmash.load_one_signature(query_ss_json)
        print(f'doing search with {query}')
        results = db.find(search_fn, query)
        results = list(results)
        results.sort(key = lambda x: -x.score)

        retval = []
        for _, sr in zip(range(LIMIT), results):
            sr_json = sourmash.save_signatures([sr.signature]).decode('utf-8')
            tup = (sr.score, sr_json, sr.location)
            retval.append(tup)

        return retval
    
test_db = sourmash.load_file_as_index('../sourmash/podar-ref.zip')
test_db = test_db.select(ksize=31)

db = ServedIndex(test_db)

@method
def select(ksize=None):
    return db.select(ksize=ksize)

@method
def find(database_id=0, search_type=None, best_only=False, threshold=0.0,
         query_ss_json=None):
    return db.find(database_id, search_type, best_only, threshold,
                   query_ss_json)

@method
def check_is_sourmash():
    return True

if __name__ == "__main__":
    print('serving on port 5000')
    serve(port=5000)
