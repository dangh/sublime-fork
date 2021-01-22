import sublime
import sublime_plugin
import subprocess
import os


def find_vcs_root(test, dirs=(".git",), default=None):
    import os

    prev, test = None, os.path.abspath(test)
    while prev != test:
        if any(os.path.exists(os.path.join(test, d)) for d in dirs):
            return test
        prev, test = test, os.path.abspath(os.path.join(test, os.pardir))
    return default


def open_fork(path, args):
    args = ["/Applications/Fork.app/Contents/Resources/fork_cli", "--git-dir={}".format(find_vcs_root(path))] + args
    print("open_fork:", args)
    subprocess.Popen(args)


class ForkOpenRepoCommand(sublime_plugin.ApplicationCommand):
    def run(self, paths=None):
        folders = sublime.active_window().folders()
        path = None
        if paths:
            path = paths[0]
        elif folders != []:
            path = folders[0]
        if path:
            open_fork(path, ["open", path])


class ForkViewHistoryCommand(sublime_plugin.ApplicationCommand):
    def run(self, **kwargs):
        path = self.get_path(**kwargs)
        if path:
            open_fork(path, ["log", "--", path])

    def get_path(self, files=None, dirs=None, paths=None):
        if paths:
            return paths[0]
        if files:
            return files[0]
        if dirs:
            return dirs[0]

    def is_enabled(self, **kwargs):
        return True if self.get_path(**kwargs) else False

    def is_visible(self, **kwargs):
        return self.is_enabled(**kwargs)


class ForkViewFileHistoryCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        if len(self.view.file_name()) > 0:
            file_name = self.view.file_name()
            open_fork(file_name, ["log", "--", file_name])

    def is_enabled(self):
        return self.view.file_name() is not None and len(self.view.file_name()) > 0
