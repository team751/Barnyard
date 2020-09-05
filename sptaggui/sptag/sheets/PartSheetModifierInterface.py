from abc import ABCMeta, abstractmethod


class PartSheetModifierInterface:
    __metaclass__ = ABCMeta
    
    @abstractmethod
    def add_part(self, part_info):
        raise NotImplementedError
    
    @abstractmethod
    def delete_part(self, part_info):
        raise NotImplementedError
    
    @abstractmethod
    def edit_part(self, part_info):
        raise NotImplementedError

    @abstractmethod 
    def get_part_info(self, uid):
        raise NotImplementedError
    
    @abstractmethod
    def search_for_parts(self, name=None, description=None, location=None):
        raise NotImplementedError
