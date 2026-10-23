import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Load the CSV file
df = pd.read_csv("vn100_data.csv")

# Create an output folder
output_dir = Path("output")
output_dir.mkdir(parents=True, exist_ok=True)

# Define sensor data groups
groups = {
    "Acceleration": ["accel_x", "accel_y", "accel_z"],
    "Angular_Velocity": ["gyro_x", "gyro_y", "gyro_z"],
    "Orientation": ["yaw_deg", "pitch_deg", "roll_deg"],
    "Magnetic_Field": ["mag_x", "mag_y", "mag_z"],
}

# Generate and save each visualization
for title, columns in groups.items():
    fig, ax = plt.subplots(figsize=(12, 5))

    for column in columns:
        ax.plot(df["timestamp_seconds"], df[column], label=column)

    ax.set_title(f"VN-100 {title.replace('_', ' ')} Over Time")
    ax.set_xlabel("Time (seconds)")
    ax.set_ylabel("Sensor Reading")
    ax.legend()
    ax.grid(True, alpha=0.3)

    fig.tight_layout()

    # Save the graph as a high-resolution PNG
    output_path = output_dir / f"vn100_{title.lower()}.png"
    fig.savefig(output_path, dpi=300, bbox_inches="tight")

    plt.close(fig)

    print(f"Saved: {output_path}")

print("All visualizations saved successfully.")