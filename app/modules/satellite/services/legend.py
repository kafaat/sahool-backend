import matplotlib.pyplot as plt, numpy as np, io

def generate_legend_png():
    fig, ax = plt.subplots(figsize=(4, 0.5))
    gradient = np.linspace(-1, 1, 256).reshape(1, -1)
    ax.imshow(gradient, aspect='auto'); ax.set_axis_off()
    ax2 = ax.twiny(); ax2.set_xlim(-1,1)
    ax2.set_xticks([-1,-0.5,0,0.5,1])
    ax2.set_xticklabels(["-1","-0.5","0","0.5","1"])
    ax2.tick_params(axis='x', labelsize=8)
    buf = io.BytesIO(); plt.tight_layout()
    fig.savefig(buf, format="png", dpi=150, bbox_inches="tight", pad_inches=0.05)
    plt.close(fig); buf.seek(0)
    return buf.getvalue()
