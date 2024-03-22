
class DEM:

    def __init__(self):

        from osgeo import gdal
        import numpy as np
        from stl import mesh

        # Open the DEM file
        dem_dataset = gdal.Open('dem_file.tif')

        # Read the DEM data into a numpy array
        dem_array = dem_dataset.ReadAsArray()

        # Normalize the elevation data
        normalized_dem = (dem_array - dem_array.min()) / (dem_array.max() - dem_array.min())

        # Create a mesh grid
        x, y = np.meshgrid(np.arange(normalized_dem.shape[1]), np.arange(normalized_dem.shape[0]))

        # Create the vertices for the STL
        vertices = np.dstack((x, y, normalized_dem)).reshape(-1, 3)

        # Define the faces of the mesh
        faces = []

        # Loop to create faces based on vertices
        for i in range(normalized_dem.shape[0] - 1):
            for j in range(normalized_dem.shape[1] - 1):
                # Define vertices for the two triangles that make up each square in the grid
                v0 = i * normalized_dem.shape[1] + j
                v1 = v0 + 1
                v2 = v0 + normalized_dem.shape[1]
                v3 = v2 + 1
                # Add the two triangles to the faces list
                faces.append([v0, v1, v2])
                faces.append([v1, v3, v2])

        # Create the mesh
        dem_mesh = mesh.Mesh(np.zeros(len(faces), dtype=mesh.Mesh.dtype))

        # Assign the vertices and faces to the mesh
        for i, f in enumerate(faces):
            for j in range(3):
                dem_mesh.vectors[i][j] = vertices[f[j], :]

        # Save the mesh to an STL file
        dem_mesh.save('dem_mesh.stl')

if __name__ == "__main__":
