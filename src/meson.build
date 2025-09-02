pkgdatadir = get_option('prefix') / get_option('datadir') / meson.project_name()
moduledir = pkgdatadir / 'thoughts'
gnome = import('gnome')


blueprint_files = [
  'ui/window.blp',
  'ui/thought_widget.blp',
  'ui/tag_widget.blp',
  'ui/canvas_screen.blp',
  'ui/intro_page.blp',
  'ui/filter_widget.blp',
]

blueprints = custom_target('blueprints',
  input: blueprint_files,
  output: '.',
  command: [find_program('blueprint-compiler'), 'batch-compile', '@OUTPUT@', '@CURRENT_SOURCE_DIR@', '@INPUT@'],
)


gnome.compile_resources('thoughts',
  'thoughts.gresource.xml',
  gresource_bundle: true,
  install: true,
  install_dir: pkgdatadir,
  dependencies: blueprints,
)

python = import('python')

conf = configuration_data()
conf.set('PYTHON', python.find_installation('python3').full_path())
conf.set('VERSION', meson.project_version())
conf.set('localedir', get_option('prefix') / get_option('localedir'))
conf.set('pkgdatadir', pkgdatadir)

configure_file(
  input: 'thoughts.in',
  output: 'thoughts',
  configuration: conf,
  install: true,
  install_dir: get_option('bindir'),
  install_mode: 'r-xr-xr-x'
)

thoughts_sources = [
  '__init__.py',
  'main.py',
]

install_data(thoughts_sources, install_dir: moduledir)
install_subdir('ui', install_dir: moduledir)
install_subdir('lib', install_dir: moduledir)