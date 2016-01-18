import bpy
import bmesh

import os
# filePath = 'F:/BLENDER_playground/houdini_hips/geo/simple_quad.obj'



def readObjFile(filePath):
    print("loading : %s" % (filePath))
    lines = []
    f = open(filePath,'r')
    while True :
        line = f.readline()
        if not line:
            break
        lines.append(line)
    
    f.close()
    
    return lines


def createMeshFromObjFile(filePath):
    objName, ext = os.path.splitext(os.path.basename(filePath))
    data = readObjFile(filePath)

    points  = []
    verts = []
    prims = []

    for line in data:
        str = line.strip()
        if str[:2] == 'v ':
            list = str.split('v ')[1].strip().split(' ')
            tup = (float(list[0]),float(list[2])*-1,float(list[1]))
            points.append(tup)
        elif str[:2] == 'vt':
            list = str.split('vt')[1].strip().split(' ')
            tup = (float(list[0]),float(list[1]),float(list[2]))
            verts.append(tup)
        elif str[:2] == 'f ':
            prims.append(str.split('f ')[1].strip())
            
    #### manage primitives points and verts
    faces = []
    facesTex = []
    for prim in prims:
        strList = prim.split(' ')
        face = []
        faceTex = []
        for item in strList:
    #        print(item.split('/'))
            face.append(int(item.split('/')[0])-1)
            faceTex.append(int(item.split('/')[1])-1)
        faces.append([int(i) for i in face])
        facesTex.append([int(i) for i in faceTex])
        



    #print('\nPoints : %s ---> %s' % (len(points), points))        
    #
    #print('\nVerts : %s ---> %s' % (len(verts),verts))
    #print('\nFaces : %s ---> %s' % (len(faces),faces))
    #print('\nFaces Textures indices : %s ---> %s' % (len(facesTex),facesTex))
    #








    mesh = bpy.data.meshes.new(objName)
    object = bpy.data.objects.new(objName,mesh)
    object.location = bpy.context.scene.cursor_location

    obj = bpy.context.scene.objects.link(object)
    mesh.from_pydata(points,[],faces)
    #mesh.update(calc_edges=True)

    ###
    ###   UVS creation

    mesh.uv_textures.new('custom_uvs')
    bm = bmesh.new()
    bm.from_mesh(mesh)
    print(bm.faces.__len__())



    ##### ------------------------
    ##### NECESSARY !!!!########
    if hasattr(bm.faces, "ensure_lookup_table"): 
        bm.faces.ensure_lookup_table()
    ##### -------------------------


    uv_layer = bm.loops.layers.uv[0]
    print(uv_layer)

    nFaces = bm.faces.__len__()

    for fi in range(nFaces):    
        n = bm.faces[fi].loops.__len__()
        for j in range(n):
            uvs = verts[facesTex[fi][j]]
            u = uvs[0]
            v = uvs[1]

            bm.faces[fi].loops[j][uv_layer].uv = (u,v)
        
        
    bm.to_mesh(mesh)


    ### SMOOTHING

    for polygon in obj.object.data.polygons:
        polygon.use_smooth = True


    return obj

# createMeshFromObjFile(filePath)