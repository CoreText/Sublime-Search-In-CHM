import os, sublime_plugin, sublime, subprocess

def get_settings():
    chm_path  = sublime.packages_path() + '/SearchInCHM'
    settings_path = chm_path + '/Default.sublime-settings'
    return sublime.load_settings('Default.sublime-settings')


def selection(view):

    def IsNotNull(value):
        return value is not None and len(value) > 1

    def badChars(sel):
        bad_characters = [
            '/', '\\', ':', '\n', '{', '}', '(', ')',
            '<', '>', '[', ']', '|', '?', '*', ' ',
            '""', "'",
        ]
        for letter in bad_characters:
            sel = sel.replace(letter, '')
        return sel

    selection = ''
    for region in view.sel():
        selection += badChars(view.substr(region))
    if IsNotNull(selection):
        return selection
    else:
        curr_sel = view.sel()[0]
        word = view.word(curr_sel)
        selection = badChars(view.substr(word))
        if IsNotNull(selection):
            return selection
        else:
            return None
    return None

def get_word(view):
    word = None
    word = selection(view)
    return word


class SearchinchmCommand(sublime_plugin.TextCommand):

    def no_word_selected(self):
        sublime.status_message('No word was selected.')

    def run(self, edit):
        text = ''
        self.chm_file_path = sublime.load_settings('Default.sublime-settings').get('chm_file_path')

        if self.view.sel():
            for region in self.view.sel():
                text += self.view.substr(region)

        for selection in self.view.sel():
            if selection.empty():
                text = self.view.word(selection)

            text = self.view.substr(selection)

            if text == "":
                text = get_word(self.view)

            if text is None:
                self.no_word_selected()

        if text is not None:
            command = 'start hh.exe "'+ self.chm_file_path +'::/res/function.'+ text.replace('_', '-') +'.html"'
            os.system(command)
            print(text)
        else:
            sublime.status_message('Place the cursor to the word.')

