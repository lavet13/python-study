import numpy as np
import pandas as pd

# Set seed for deterministic reproducibility across student environments
np.random.seed(42)
n_samples = 2000

# 1. Generate core independent physical dimensions
full_area = np.random.lognormal(mean=3.9, sigma=0.4, size=n_samples) + 15.0 # Min area ~ 20 sqm
full_area = np.clip(full_area, 18.0, 350.0) # Realistic bounds

# Establish physical constraint: living area ~ 60% of full area with Gaussian noise
living_ratio = np.random.normal(loc=0.6, scale=0.08, size=n_samples)
living_area = full_area * np.clip(living_ratio, 0.35, 0.85)

# Establish physical constraint: kitchen area ~ 15% of full area with Gaussian noise
kitchen_ratio = np.random.normal(loc=0.15, scale=0.03, size=n_samples)
kitchen_area = full_area * np.clip(kitchen_ratio, 0.08, 0.30)

# Generate integer structures
num_rooms = np.zeros(n_samples)
for i in range(n_samples):
    if full_area[i] < 30.0:
        num_rooms[i] = 0 # Studio
    elif full_area[i] < 50.0:
        num_rooms[i] = 1
    elif full_area[i] < 80.0:
        num_rooms[i] = np.random.choice([1, 2], p=[0.3, 0.7])
    elif full_area[i] < 120.0:
        num_rooms[i] = np.random.choice([2, 3], p=[0.2, 0.8])
    else:
        num_rooms[i] = np.random.choice([3, 4, 5], p=[0.3, 0.5, 0.2])

floor = np.random.randint(1, 26, size=n_samples)
max_floors = floor + np.random.randint(0, 15, size=n_samples)

# Spatial metrics
metro_distance_km = np.random.exponential(scale=2.5, size=n_samples)
metro_distance_km = np.clip(metro_distance_km, 0.1, 25.0)

# Categorical allocations
regions = np.random.choice(['Moscow', 'New_Moscow', 'Moscow_Oblast'], size=n_samples, p=[0.55, 0.20, 0.25])
renovations = np.random.choice(['None', 'Cosmetic', 'Euro', 'Designer'], size=n_samples, p=[0.20, 0.45, 0.25, 0.10])
building_types = np.random.choice(['Panel', 'Brick', 'Monolith'], size=n_samples, p=[0.40, 0.35, 0.25])

# Temporal vector: Transaction listings spanning 2024-01-01 to 2026-05-01
start_date = pd.to_datetime('2024-01-01')
end_date = pd.to_datetime('2026-05-01')
time_deltas = np.random.randint(0, int((end_date - start_date).total_seconds()), size=n_samples)
timestamps = start_date + pd.to_timedelta(time_deltas, unit='s')

# 2. Mathematical Price Generation (Base logic + physical interactions)
# Baseline price per square meter in Moscow: ~250,000 RUB
base_m2_price = 250000.0

# Apply regional scaling coefficients
region_coeff = {'Moscow': 1.0, 'New_Moscow': 0.75, 'Moscow_Oblast': 0.55}
r_coeffs = np.array([region_coeff[r] for r in regions])

# Apply renovation scaling coefficients
renovation_coeff = {'None': 0.85, 'Cosmetic': 1.0, 'Euro': 1.18, 'Designer': 1.40}
ren_coeffs = np.array([renovation_coeff[rn] for rn in renovations])

# Apply structural quality coefficients
build_coeff = {'Panel': 0.90, 'Brick': 1.05, 'Monolith': 1.20}
b_coeffs = np.array([build_coeff[b] for b in building_types])

# Proximity premium: Exponential decay of price as distance to metro increases
metro_decay = np.exp(-0.08 * metro_distance_km)

# Compute target regression price with multi-factor multiplicative interactions + Gaussian noise
noise = np.random.normal(loc=1.0, scale=0.12, size=n_samples)
price_rub = (full_area * base_m2_price) * r_coeffs * ren_coeffs * b_coeffs * (0.7 + 0.3 * metro_decay) * noise

# Format prices to realistic integers
price_rub = np.round(price_rub, -4)

# 3. Inject Missing Values (MAR and MCAR) to test pre-processing
mask_living = np.random.rand(n_samples) < 0.10 # 10% MCAR missing
living_area[mask_living] = np.nan

mask_kitchen = np.random.rand(n_samples) < 0.08 # 8% MCAR missing
kitchen_area[mask_kitchen] = np.nan

mask_metro = np.random.rand(n_samples) < 0.05 # 5% MCAR missing
metro_distance_km[mask_metro] = np.nan

# Categorical missingness: 5% of renovations are missing
mask_renovation = np.random.rand(n_samples) < 0.05
renovations_with_nan = renovations.astype(object)
renovations_with_nan[mask_renovation] = np.nan

# 4. Inject Realistic Anomalies and Outliers to test robust scaling and filtering
# Anomaly Type A: Unphysical structural overlap (Living Area > Full Area)
anomaly_idx_a = np.random.choice(n_samples, size=10, replace=False)
for idx in anomaly_idx_a:
    living_area[idx] = full_area[idx] * 1.15  # Impossible physical state

# Anomaly Type B: Extreme luxury estate pricing outliers
anomaly_idx_b = np.random.choice(n_samples, size=5, replace=False)
for idx in anomaly_idx_b:
    price_rub[idx] = price_rub[idx] * 6.5  # Artificial extreme pricing outlier

# Anomaly Type C: Zero-value kitchen area anomalies in high-end properties
anomaly_idx_c = np.random.choice(n_samples, size=8, replace=False)
for idx in anomaly_idx_c:
    kitchen_area[idx] = 0.0

# 5. Define Classification Target: Ordinal Price Segments
# Calculate clean boundaries on original baseline to ensure mathematical modeling capability
q33, q66 = np.percentile(price_rub, [33.3, 66.6])
price_segment = np.where(price_rub <= q33, 'Budget', np.where(price_rub <= q66, 'Standard', 'Premium'))

# 6. Assemble Final Dataframe and Export
dataset = pd.DataFrame({
    'id': np.arange(1, n_samples + 1),
    'timestamp': timestamps,
    'full_area': np.round(full_area, 1),
    'living_area': np.round(living_area, 1),
    'kitchen_area': np.round(kitchen_area, 1),
    'floor': floor,
    'num_rooms': num_rooms.astype(int),
    'metro_distance_km': np.round(metro_distance_km, 3),
    'region': regions,
    'renovation': renovations_with_nan,
    'building_type': building_types,
    'price_rub': price_rub,
    'price_segment': price_segment
})

dataset.to_csv('moscow_housing_study.csv', index=False)
