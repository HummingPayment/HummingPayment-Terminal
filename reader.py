import cffi

ffi = cffi.FFI()

ffi.cdef('''
void * create_context();
void destroy_context(void *);
char * read_uid(void *);
''')

class Reader():
    def __init__(self):
        try:
            self.lib = ffi.dlopen("./reader_support/read_uid.so")
        except OSError:
            print("ATTENTION: You need to compile code under ./reader_support/ first.")
        finally:
            raise RuntimeError

    def _read_uid(self):
        cxt = self.lib.create_context()
        try:
            result = ffi.string(self.lib.read_uid(cxt))
        except RuntimeError:
            result = None
        self.lib.destroy_context(cxt)
        return result

    def _format_card_id(self, uid):
        card_id = uid.decode("utf-8")
        card_id = card_id.upper()
        return card_id

    def get_card_id(self):
        return self._format_card_id(self._read_uid())
