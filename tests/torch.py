float16 = "float16"
float32 = "float32"


class cuda:
    @staticmethod
    def is_available():
        return False

    class amp:
        @staticmethod
        def autocast(dtype=None):
            class _Ctx:
                def __enter__(self):
                    return None

                def __exit__(self, exc_type, exc, tb):
                    return False

            return _Ctx()
