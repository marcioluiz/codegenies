# utils/pattern_matching.py

class PatternMatching:
    """
    Class containing patterns for the matching operations.
    """

    def filename_matching_patterns(self):
        """
        List of common file name matching patterns with "#".

        Returns:
             - array[]: List of matching patterns with "#".
        """
        # Patterns list to be tested along with the right group indexes to be extracted
        patterns = [
            # 4. "##folder1/folder2/filename.ext" or "##folder1/folder2-name/filename.ext" and ending "filename.ext" or "filename.ext"
            (r'##(((\w+)\/(\w+\D\w+))|((\w+)\/(\w+\D\w+)\/(\w+\D\w+)))\/((\w+\D\w+\D\w+|\w+\D\w+\D\w+\D\w+)(\.)([a-z]{2}|[a-z]{3})\b)', 9),
            # 3. "##folder/file.ext" or "##folder-name/file.ext" and ending "file-name.ext" or "file-name.ext"
            (r'##((\w+\D\w+))\/(((\w+\D\w+)|(\w+\D\w+\D\w+))(\.)([a-z]{2}|[a-z]{3})\b)', 3),
            # 2. "##foldername/filename.ext" or "##folder-name/filename.ext" 
            (r'##((\w+\D\w+))\/((\w+)(\.)([a-z]{2}|[a-z]{3})\b)', 3),
            # 1. "##foldername/filename.module.ext" or "##folder-name/filename.module.ext" 
            (r'##((\w+\D\w+))\/((\w+)(\.)((\w+)(\.)([a-z]{2}|[a-z]{3})\b)', 3),
            # 1. "##filename.ext"
            (r'##(((\w+)|(\w+\-\w+))(\.)([a-z]{2}|[a-z]{3})\b)', 1)
        ]
        return patterns
    
    def filename_matching_patterns_no_hashtag(self):
        """
        List of common file name matching patterns without "#".

        Returns:
             - array[]: List of matching patterns without "#".
        """
        # Patterns list to be tested along with the right group indexes to be extracted
        patterns = [
            # 4. "folder1/folder2/filename.ext" or "folder1/folder2-name/filename.ext" and ending "filename.ext" or "filename.ext"
            (r'(((\w+)\/(\w+\D\w+))|((\w+)\/(\w+\D\w+)\/(\w+\D\w+)))\/((\w+\D\w+\D\w+|\w+\D\w+\D\w+\D\w+)(\.)([a-z]{2}|[a-z]{3})\b)', 9),
            # 3. "folder/file.ext" or "folder-name/file.ext" and ending "file-name.ext" or "file-name.ext"
            (r'((\w+\D\w+))\/(((\w+\D\w+)|(\w+\D\w+\D\w+))(\.)([a-z]{2}|[a-z]{3})\b)', 3),
            # 2. "foldername/filename.ext" or "folder-name/filename.ext" 
            (r'((\w+\D\w+))\/((\w+)(\.)([a-z]{2}|[a-z]{3})\b)', 3),
            # 1. "foldername/filename.module.ext" or "folder-name/filename.module.ext" 
            (r'((\w+\D\w+))\/((\w+)(\.)((\w+)(\.)([a-z]{2}|[a-z]{3})\b)', 3),
            # 0. "filename.ext"
            (r'(((\w+)|(\w+\-\w+))(\.)([a-z]{2}|[a-z]{3})\b)', 1)
        ]
        return patterns
    
    def foldername_matching_patterns(self):
        """
        List of common folder name matching patterns with "#".

        Returns:
             - array[]: List of matching patterns with "#".
        """
        # List of folder name patterns to test
        patterns = [
            # 1. "##folder/filename"
            (r'##(\w+)\/(\w+)', 0),
            # 2. "##folder-name/filename"
            (r'##(\w+)-(\w+)\/(\w+)', 1),
            # 3. "##folder1/folder2/filename"
            (r'##(\w+)\/(\w+)\/(\w+)', 2),
            # 4. "##folder1/folder2-name/filename"
            (r'##(\w+)\/(\w+)-(\w+)\/(\w+)', 3)
        ]
        return patterns
    
    def comment_styles_list(self):
        """
        List of common file comment styles for different programming languages

        Returns:
            - object{}: List maping of comment styles.
        """
        comment_styles = {
                'css': {'single': '//', 'multi_start': '/*', 'multi_end': '*/'},
                'html': {'single': '', 'multi_start': '<!--', 'multi_end': '-->'},
                'xml': {'single': '', 'multi_start': '<!--', 'multi_end': '-->'},
                'c': {'single': '//', 'multi_start': '/*', 'multi_end': '*/'},
                'cpp': {'single': '//', 'multi_start': '/*', 'multi_end': '*/'},
                'java': {'single': '//', 'multi_start': '/*', 'multi_end': '*/'},
                'js': {'single': '//', 'multi_start': '/*', 'multi_end': '*/'},
                'ts': {'single': '//', 'multi_start': '/*', 'multi_end': '*/'},
                'py': {'single': '#', 'multi_start': '"""', 'multi_end': '"""'},
                'rb': {'single': '#', 'multi_start': '=begin', 'multi_end': '=end'},
                'sh': {'single': '#', 'multi_start': '', 'multi_end': ''},
                'php': {'single': '//', 'multi_start': '/*', 'multi_end': '*/'},
                'go': {'single': '//', 'multi_start': '/*', 'multi_end': '*/'},
                'swift': {'single': '//', 'multi_start': '/*', 'multi_end': '*/'},
                'scala': {'single': '//', 'multi_start': '/*', 'multi_end': '*/'},
                'lua': {'single': '--', 'multi_start': '--[[', 'multi_end': ']]'},
                'vb': {'single': "'", 'multi_start': '', 'multi_end': ''},
                'vbs': {'single': "'", 'multi_start': '', 'multi_end': ''},
                'v': {'single': '//', 'multi_start': '/*', 'multi_end': '*/'},
                'vhd': {'single': '--', 'multi_start': '', 'multi_end': ''},
                'fsharp': {'single': '//', 'multi_start': '(*', 'multi_end': '*)'},
                'lisp': {'single': ';', 'multi_start': '#|', 'multi_end': '|#'},
                # Adicione mais linguagens conforme necessário
            }
        return comment_styles
    
    def language_extensions_list(self):
        """
        List of common file extensions for different programming languages

        Returns:
            - array[]: List of extensions.
        """
        # List of common file extensions for different programming languages
        language_extensions = [
                'apl', 'asm', 'awk', 'bas', 'bat', 'c', 'clj', 'coffee', 'cpp', 'cr', 'd', 'dart',
                'ex', 'f77', 'f95', 'forth', 'fsharp', 'go', 'groovy', 'hs', 'html', 'java', 'jl',
                'js', 'kt', 'lisp', 'lua', 'm', 'ml', 'php', 'pl', 'pro', 'ps1', 'py', 'rb', 'r',
                'scala', 'scm', 'sh', 'sql', 'st', 'swift', 'ts', 'vb', 'v', 'vbs', 'vim', 'vhd',
                'xml'
            ]
        return language_extensions
    

    