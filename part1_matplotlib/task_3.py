import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as patches
def main():
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.set_xlim(0,100)
    ax.set_ylim(0,100)
    sky =patches.Rectangle((0, 0), 100, 100, color="#87CEEB")
    ground = patches.Rectangle((0, 0), 100, 20, color="#2E8B57")
    building = patches.Rectangle((70, 20), 30, 50, color="#CD5C5C")
    window1 = patches.Rectangle((75, 55), 11, 12, facecolor="#FFFFE0", edgecolor="black")
    window2 = patches.Rectangle((75, 30), 11, 12, facecolor="#FFFFE0", edgecolor="black")
    sun=patches.Circle((20, 85), 10, color="#FFD700")
    root=patches.Polygon([[60, 70], [80, 90], [100, 90], [100, 70]], color="#8B0000" )
    cloud1=patches.Ellipse((55, 85), 35, 15, color="white", alpha=0.9)
    cloud2 = patches.Ellipse((20, 50), 35, 10, color="white", alpha=0.7)
    all_patches = [
        sky, ground, sun, cloud1,
        cloud2, building, window1, window2,
        root
    ]
    for patch in all_patches:
        ax.add_patch(patch)

    ax.axis('off')
    plt.savefig("img/task3.png", bbox_inches="tight")
    plt.show()
if __name__ == "__main__":
    main()
