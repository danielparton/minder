import os
import yaml
import subprocess


class DotFile(object):
    def __init__(self):
        self.dot_filename = '.mindr'
        user_home_dir = os.path.expanduser('~')
        self.dot_filepath = os.path.join(user_home_dir, self.dot_filename)
        with open(self.dot_filepath) as dot_file:
            dotfile_data = yaml.load(dot_file)
        self.project_dir = dotfile_data.get('project_dir')
        self.viewer_path = dotfile_data.get('viewer_path')
        self.editor_path = dotfile_data.get('editor_path')


dotfile = DotFile()


class MindrDB(object):
    """
    Member variables
    ----------------
    notes: dict
        notename: tags: tag
    tags: set
        set(tags)
    notes_by_tag: dict
    """
    def __init__(self):
        self.config = DotFile()
        # TODO This is a tmp hack
        self.notes_dirpath = os.path.join(self.config.project_dir, 'notes/work')
        # self.notes_dirpath = os.path.join(self.config.project_dir, 'notes/.personal')
        self.private_notes_dirpath = os.path.join(self.config.project_dir, 'notes/.personal')
        self.anthologies_dirpath = os.path.join(self.config.project_dir, 'anthologies')

        self.get_note_filepaths()
        self.get_metadata()
        self.populate_notes_by_tag()

    def get_note_filepaths(self):
        self.note_filepaths = [
            os.path.join(self.notes_dirpath, filename) for filename in os.listdir(self.notes_dirpath)
            if (len(filename) > 4 and filename[-4:] == '.txt')
        ]

    def get_metadata(self):
        notes = {}
        tags = set()
        for note_filepath in self.note_filepaths:
            note_filename = os.path.basename(note_filepath)
            note_name = note_filename[: note_filename.index('.txt')]
            notes.update({note_name: {}})
            note_tags = []

            with open(note_filepath, encoding='utf-8') as note_file:
                try:
                    for line in note_file:
                        if line == '':
                            break
                        if len(line) >= 5 and line[0:5] == '@tag:':
                            note_tags.append(line[5:].strip())
                except UnicodeDecodeError:
                    print('Warning: invalid character detected in note - {}'.format(note_name))

            tags.update(note_tags)
            notes[note_name].update({'tags': note_tags})

        self.notes = notes
        self.tags = tags

    def populate_notes_by_tag(self):
        notes_by_tag = {}
        for notename, note in self.notes.items():
            for tag in note['tags']:
                if tag in notes_by_tag:
                    notes_by_tag[tag].append(notename)
                else:
                    notes_by_tag[tag] = [notename]
        self.notes_by_tag = notes_by_tag

    def mk_new_note(self, notename):
        if notename in self.notes:
            print('Note {} already exists. Exiting.'.format(notename))
        else:
            fpath = os.path.join(self.notes_dirpath, notename)
            subprocess.check_output('{} {} >/dev/tty'.format(self.config.editor_path, fpath), shell=True)

