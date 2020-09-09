import os, shutil

class Context:
  defaultConfig = {'sizes': []}
  def __init__(self, src, width=0, height=0):
    self.src = src
    self._init_config(width, height)
    self._init_src_folders()

  def run(self):
    for i, ctx in enumerate(self.config['sizes']):
      print(f'{i+1} / {len(self.config["sizes"])}, {ctx["path"]}')
      self.run_with(ctx)

  def run_with(self, ctx):
    from resize import validate_path, resize_and_crop
    for s in self.srcs:
      abss = self._abstract_src(s)
      ss = sorted([s for s in os.listdir(abss) if s.lower().endswith('jpg') or s.lower().endswith('jpeg')])
      dst = validate_path(os.path.sep.join([self.config["dest"], s, ctx["path"].replace('/', os.path.sep)]))
      [resize_and_crop(os.path.sep.join([abss, s]), os.path.sep.join([dst, s]), ctx["size"]) for s in ss[:(ctx['count'] if ctx['count'] > 0 else len(ss))]]
      
  def _abstract_src(self, s):
    return f'{self.src}{os.path.sep}{s}'

  def _init_config(self, width=0, height=0):
    import json
    self.config = Context.defaultConfig
    p = self.src + (os.path.sep if not self.src.endswith(os.path.sep) else '') + 'config.json'
    if os.path.exists(p):
      with open(p, 'r', encoding='utf-8') as f:
        self.config.update(json.loads(f.read()))
    w, h = int(width), int(height)
    if w * h > 0:
      self.config["sizes"].append({'size': [w, h], 'count': 0, 'path': f'{w}x{h}'})
    self.config['dest'] = self.config.get('dest', self.src)
    self.config['dest'] = self.src + os.path.sep + self.config['dest'] if self.config['dest'].startswith('.') else self.config['dest']

  def _init_src_folders(self):
    self.srcs = sorted([s for s in os.listdir(self.src) if os.path.isdir(f'{self.src}{os.path.sep}{s}')])