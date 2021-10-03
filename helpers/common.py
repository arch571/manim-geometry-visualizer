def flattenList(l):
  return [ l2 for l1 in l for l2 in l1]

def flattenRenderList(l):
    return flattenList([ l1["mo_list"] for l1 in l])

def playRenderGroup(scene, render_group):
  anim_method = render_group["anim_method"]
  mode = render_group["mode"]
  run_time = render_group["run_time"]
  print(render_group)
  if mode == "parallel":
    play_list = [ anim_method(mo, run_time=run_time) for mo in render_group["mo_list"] ]
    scene.play(*play_list)
    scene.wait()
  else: ##serial
    for mo in render_group["mo_list"]:
      scene.play(anim_method(mo, run_time=run_time))
      scene.wait()
