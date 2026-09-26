from helpers.config import Settings , get_settings

from pathlib import Path

import os

import string

import random

class BaseController:
    def __init__(self):
        self.app_settings = get_settings()
        self.file_path = Path(__file__).parent.parent / 'assets' / 'files'
    
    def generate_random_string(self , length: int=12):
        return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

        
        