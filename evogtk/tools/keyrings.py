# -*- coding: utf-8 -*-
###############################################################################
# (C) 2012 Oliver Gutiérrez
###############################################################################
"""
:mod:`evogtk.tools.keyrings` -- 
===================================

.. module:: evogtk.tools.keyrings
    :platform: 
    :synopsis: Gnome keyring utility class
    :deprecated:
.. moduleauthor:: Oliver Gutiérrez

"""

# Tutorial for gnome keyring at http://www.mindbending.org/bending-gnome-keyring-with-python-part-1/ 

# Glib and Gnome imports
import gnomekeyring as gk


class KeyringManager(object):
    """
    Gnome keyring manager class
    """

    SECRET=gk.ITEM_GENERIC_SECRET
    NETWORK=gk.ITEM_NETWORK_PASSWORD
    NOTE=gk.ITEM_NOTE
    
    def __init__(self):
        """
        Initialization method
        """
        pass
    
    def get_keyrings(self):
        """
        Return keyring names list
        """
        return gk.list_keyring_names_sync()

    def search_key(self,query):
        """
        Search for a key into the keyrings using query parameters
        """
        try:
            result_list = gk.find_items_sync(gk.ITEM_GENERIC_SECRET, query)
        except gk.NoMatchError:
            return None
        
        return result_list
        # TODO; Adjust results list data    
        # secrets = [result.secret for result in result_list]
        # if len(secrets) == 1:
        #    secrets = secrets[0]
        # return secrets
    
    def dump(self):
        """
        Dumps all keys in keyrings into a tuple list of name/secret
        """
        secrets=[]
        for N in gk.list_keyring_names_sync():
            for I in gk.list_item_ids_sync(N):
                info=gk.item_get_info_sync('login',I)
                secrets.append((info.get_display_name(),info.get_secret()))
        return secrets

    def remove_key(self,keyring,query):
        """
        Removes a key from an specified keyring that matches specified query
        """
        key=self.search_key(query)
        if key:
            # TODO: Get keyring and key id from result
            gk.item_delete_sync(keyring,id)
        else:
            raise

    def remove_keyring(self,keyring):
        """
        Remove a keyring by its name
        """
        gk.delete_sync(keyring)

    def create_keyring(self,keyring,password):
        """
        Create a new keyring with given name and password
        """
        gk.create_sync(keyring,password)

    def create_key(self,keyring,name,attribs,secret,type=SECRET,update=True):
        """
        Create a new key into specified keyring
    
        :param keyring: Keyring name this item will belong
        :type keyring: string
        
        :param name: Unique key name inside the keyring
        :type name: string
        
        :param attribs: Dictionary with custom data
        :type attribs: dict


        :param secret: What we need to store secretly
        :type secret: string

        :param type: Describes the item that is being added. Can be SECRET, NETWORK and NOTE
        :type type: int

        :param update: If exist a previous item with same name and attributes it will be updated
        :type update: bool

        .. note:: Data stored with attribs parameter is mainly used for finding them later with search_key method
        """

        pass

