class AppModuleImportError(ImportError):
    """
    An app submodule raised an ImportError.
    """


class AppImportError(ImportError):
    """
    An app raised an ImportError.
    """


class AppCommandError(Exception):
    """
    A command error.
    """


class SessionStorageDoesNotExist(Exception):
    """
    An invalid session storage name was provided.
    """


class SessionSecretKeyDoesNotExist(Exception):
    """
    A secret was not provided to the encrypted cookie session storage.
    """


class AppRouteURLKeyError(KeyError):
    """
    An app route was constructed without required keyword match arguments.
    """
