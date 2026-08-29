import os
import json

base_dir = r"c:\Users\harih\Zensec\frontend\src"

files = {
    "app/threats/page.tsx": """export default function ThreatsPage() {
  return (
    <div className="flex flex-col items-center justify-center h-[60vh] text-center space-y-4">
      <h1 className="text-3xl font-bold text-white">Threat Intelligence</h1>
      <p className="text-zinc-400 max-w-lg">Advanced IOC enrichment and threat actor analysis is processing in the backend. Threat Intel feeds are currently being loaded.</p>
    </div>
  );
}""",
    "app/analytics/page.tsx": """export default function AnalyticsPage() {
  return (
    <div className="flex flex-col items-center justify-center h-[60vh] text-center space-y-4">
      <h1 className="text-3xl font-bold text-white">Security Analytics & ML Models</h1>
      <p className="text-zinc-400 max-w-lg">Scikit-learn Anomaly Detection and Isolation Forest algorithms are calculating baseline behaviors...</p>
    </div>
  );
}""",
    "app/assets/page.tsx": """export default function AssetsPage() {
  return (
    <div className="flex flex-col items-center justify-center h-[60vh] text-center space-y-4">
       <h1 className="text-3xl font-bold text-white">Asset Inventory</h1>
       <p className="text-zinc-400 max-w-lg">Discovering networked assets, endpoints, and identity providers.</p>
    </div>
  );
}"""
}

for path, content in files.items():
    full_path = os.path.join(base_dir, path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content)
print("Stub pages generated successfully.")
