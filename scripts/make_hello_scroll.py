import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import vesuvius

SCAN_ID = "Scroll1"
Z = 1000
Y0, Y1 = 3520, 3584
X0, X1 = 4256, 4320
OUT = "outputs/hello_scroll.png"

def main():
    volume = vesuvius.Volume(SCAN_ID)
    img = volume[Z, Y0:Y1, X0:X1]
    plt.imshow(img, cmap="gray")
    plt.axis("off")
    plt.savefig(OUT, dpi=200, bbox_inches="tight", pad_inches=0)
    print({
        "scan_id": SCAN_ID,
        "z": Z,
        "y_range": [Y0, Y1],
        "x_range": [X0, X1],
        "shape": list(np.shape(img)),
        "output": OUT,
    })

if __name__ == "__main__":
    main()
