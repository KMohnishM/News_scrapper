#!/usr/bin/env bash
set -euo pipefail

echo "🚀 1/5  Installing nvm & Node 20 (if missing)…"
if ! command -v nvm >/dev/null 2>&1; then
  curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash
  export NVM_DIR="$HOME/.nvm"
  source "$NVM_DIR/nvm.sh"
fi
nvm install --lts=hydrogen   # Node 20 LTS
nvm use --lts=hydrogen
nvm alias default 20

echo "📦 2/5  Ensuring npm project exists…"
if ! [ -f package.json ]; then
  npm init -y
fi

echo "🛠 3/5  Installing Tailwind + PostCSS deps…"
npm install -D tailwindcss postcss autoprefixer

echo "🧹 4/5  Cleaning old/empty config stubs…"
for f in tailwind.config.js postcss.config.js; do
  if [ -f "$f" ]; then
    # If file size ≤ 5 bytes → probably the empty placeholder Cursor created
    if [ "$(stat -c%s "$f")" -le 5 ]; then
      echo "  ↪︎  removing stale $f"
      rm "$f"
    else
      ts=$(date +%s)
      echo "  ↪︎  backing up existing $f → $f.$ts.bak"
      mv "$f" "$f.$ts.bak"
    fi
  fi
done

echo "⚙️ 5/5  Generating fresh configs…"
npx --yes tailwindcss@latest init -p

# Add sensible content globs to tailwind.config.js
sed -i '5 i\  content: ["./src/**/*.{js,ts,jsx,tsx}"],' tailwind.config.js

# Create a default globals.css with Tailwind directives
mkdir -p src
cat > src/globals.css <<'TAILWIND'
@tailwind base;
@tailwind components;
@tailwind utilities;
TAILWIND

echo -e "\n✅  Done!  Tailwind is wired up.\n"
echo "Next steps:"
echo "  • import \"../src/globals.css\" at the top of your Next .js root (e.g. app/layout.tsx or pages/_app.tsx)."
echo "  • run:  npm run dev"

