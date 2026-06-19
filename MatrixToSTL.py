import json
import trimesh
import helpers
import numpy as np

if __name__=="__main__":
    import sys
    if len(sys.argv)<3:
        print("Usage: python MatrixToSTL.py <input_dir> <output_dir> <mountain --or-- hole (optional, defaults to mountain)> <LpNorm (optional, for redistribution)>")
    input_dir = sys.argv[1]
    output_dir = sys.argv[2]
    LpNorm = 2
    base_height = -.05
    if len(sys.argv)>3:
        if sys.argv[3]!='mountain':
            base_height = .55

    if len(sys.argv)>4:
        LpNorm = float(sys.argv[4])

    print("Loading Heightmap...")
    save_location = open(input_dir)
    ETMatrix = json.load(save_location)

    #We will normalize the matrix to having values between 0 and 1, first linearly, and then redistributing using the function above
    ETMatrix = helpers.normalizeMatrix(ETMatrix,LpNorm)

    rows = len(ETMatrix)
    cols = len(ETMatrix[0])

    aspectRatio = cols/rows

    # ==========================================
    # 1. Build the top mesh.
    # ==========================================

    #Build the grid, by using linspace to subdivide x and y axes, and meshgrid to turn them into every set of ordered pairs
    x = np.linspace(0,aspectRatio,cols)
    y = np.linspace(0,1,rows)
    xx,yy = np.meshgrid(x,y)

    zz = .5*np.array(ETMatrix)

    #Now flatten and use column stack to turn into a set of triples.  These are your vertices.
    vert = np.column_stack((xx.flatten(),yy.flatten(),zz.flatten()))

    #How do we get faces?  First assign every vertex a number between 0 and width*height.  We can make this as a matrix which will ahve the right number in the ij entry as follows:
    grid_indices = np.arange(rows*cols).reshape(rows,cols)

    #So now vert[grid_indices[i][j]] should get the vertex number for the ij position of the grid.  We don't actually need to call vert on this, but it gives a nice geometric picture for our vertex numbering

    #Now these pluck out the possible top_left indices by covering the bottom row and right column, and similarly for the rest
    top_left = grid_indices[:-1, :-1].flatten()
    top_right = grid_indices[:-1, 1:].flatten()
    bottom_left = grid_indices[1:, :-1].flatten()
    bottom_right = grid_indices[1:, 1:].flatten()

    #From here we can form two triangles for every index.  Winding order should face up.
    tri1 = np.column_stack((top_left,top_right,bottom_left))
    tri2 = np.column_stack((top_right,bottom_right,bottom_left))

    #Since these are just lists of triangles given from vertex indices (which correspond to vert), we can make them our face list.
    top_faces = np.vstack((tri1,tri2))

    # ==========================================
    # 2. Build the bottom mesh.
    # ==========================================
    
    # This will just copy the top mesh, and reverse the normals, using a height of base_height rather than ETMatrix
    bottom_vert = vert.copy()
    bottom_vert[:,2] = base_height
    bottom_start = len(vert)

    #All vertices are either on the top or the bottom
    vertices = np.vstack((vert,bottom_vert))

    #To make the mesh, let's just use the same triangulation as the top.  Reversing top_faces winding order to make sure it points down.
    bottom_faces = top_faces[:,::-1]+bottom_start


    # ==========================================
    # 3. Now build the boundary walls
    # ==========================================

    #We've already got all the vertices, we are just connecting the top and bottom.

    # Get the sequential index loops along the 4 borders of the grid
    top_edge = grid_indices[0, :]
    right_edge = grid_indices[:, -1]
    bottom_edge = grid_indices[-1, :][::-1]  # Flip to maintain clockwise loop
    left_edge = grid_indices[:, 0][::-1]

    # Combine into a continuous loop around the perimeter
    boundary_indices = np.concatenate([top_edge[:-1], right_edge[:-1], bottom_edge[:-1], left_edge[:-1]])
    bottom_boundary_indices = boundary_indices + bottom_start

    num_boundary_pts = len(boundary_indices)
    wall_faces = []
    
    #Now we make the wall panels around the perimeter, finding each square connecting top and bottom boundary points and splitting them into two triangles
    for i in range(num_boundary_pts):
        next_i = (i+1) % num_boundary_pts
        
        #Top boundary indices for my rectangle
        t0 = boundary_indices[i]
        t1 = boundary_indices[next_i]

        #Bottom boundary indices for my rectangle
        b0 = bottom_boundary_indices[i]
        b1 = bottom_boundary_indices[next_i]

        # Wall triangles (Winding order must face outwards)
        wall_faces.append([t0, b0, t1])
        wall_faces.append([t1, b0, b1])

    # ==========================================
    # 4. ASSEMBLE WATERTIGHT MESH
    # ==========================================
    all_faces = np.vstack((top_faces, wall_faces, bottom_faces))

    # Instantiate Trimesh object
    solid_mesh = trimesh.Trimesh(vertices=vertices, faces=all_faces)

    #If we're digging a hole, we need the normals pointing outward.
    if base_height>0:
        solid_mesh.invert()


    # Verify the object is completely sealed and 3D printable
    print(f"Is watertight solid: {solid_mesh.is_watertight}")
    print(f"Is winding consistently: {solid_mesh.is_winding_consistent}")

    # If the volume is negative, normals are inverteed
    print(f"Volume: {solid_mesh.volume}")


    # ==========================================
    # 5. Show and/or Export the file
    # ==========================================

    #This commented line shows the result in the built in trimesh viewer.
    #solid_mesh.show()
    
    print("Exporting....")
    solid_mesh.export(output_dir)
    print("Done!")

