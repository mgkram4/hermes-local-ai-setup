#!/bin/bash
# ══════════════════════════════════════════════════════════════════════════════
# HERMES SAFE UPDATE SCRIPT
# ══════════════════════════════════════════════════════════════════════════════
# Backs up your custom config before updating, then restores after.
# Run: ./scripts/safe_update.sh
# Or:  hermes safe-update (after adding the command)
# ══════════════════════════════════════════════════════════════════════════════

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
GOLD='\033[1;33m'
NC='\033[0m' # No Color

# Paths
HERMES_HOME="${HERMES_HOME:-$HOME/.hermes}"
CONFIG_FILE="$HERMES_HOME/config.yaml"
ENV_FILE="$HERMES_HOME/.env"
BACKUP_DIR="$HERMES_HOME/backups"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_SUBDIR="$BACKUP_DIR/pre_update_$TIMESTAMP"

echo -e "${GOLD}⚕ Hermes Safe Update${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo

# ── Step 1: Create backup directory ──────────────────────────────────────────
echo -e "${CYAN}→ Creating backup...${NC}"
mkdir -p "$BACKUP_SUBDIR"

# ── Step 2: Backup config files ──────────────────────────────────────────────
BACKED_UP=()

if [ -f "$CONFIG_FILE" ]; then
    cp "$CONFIG_FILE" "$BACKUP_SUBDIR/config.yaml"
    BACKED_UP+=("config.yaml")
    echo "  ✓ Backed up config.yaml"
fi

if [ -f "$ENV_FILE" ]; then
    cp "$ENV_FILE" "$BACKUP_SUBDIR/.env"
    BACKED_UP+=(".env")
    echo "  ✓ Backed up .env"
fi

# Backup custom skins
if [ -d "$HERMES_HOME/skins" ]; then
    cp -r "$HERMES_HOME/skins" "$BACKUP_SUBDIR/skins"
    BACKED_UP+=("skins/")
    echo "  ✓ Backed up skins/"
fi

# Backup custom skills
if [ -d "$HERMES_HOME/skills" ]; then
    cp -r "$HERMES_HOME/skills" "$BACKUP_SUBDIR/skills"
    BACKED_UP+=("skills/")
    echo "  ✓ Backed up skills/"
fi

# Backup memory files
if [ -f "$HERMES_HOME/MEMORY.md" ]; then
    cp "$HERMES_HOME/MEMORY.md" "$BACKUP_SUBDIR/MEMORY.md"
    BACKED_UP+=("MEMORY.md")
    echo "  ✓ Backed up MEMORY.md"
fi

if [ -f "$HERMES_HOME/USER.md" ]; then
    cp "$HERMES_HOME/USER.md" "$BACKUP_SUBDIR/USER.md"
    BACKED_UP+=("USER.md")
    echo "  ✓ Backed up USER.md"
fi

# Backup SOUL.md (persona)
if [ -f "$HERMES_HOME/SOUL.md" ]; then
    cp "$HERMES_HOME/SOUL.md" "$BACKUP_SUBDIR/SOUL.md"
    BACKED_UP+=("SOUL.md")
    echo "  ✓ Backed up SOUL.md"
fi

echo
echo -e "${GREEN}✓ Backup saved to:${NC}"
echo "  $BACKUP_SUBDIR"
echo

# ── Step 3: Run the actual update ────────────────────────────────────────────
echo -e "${CYAN}→ Running hermes update...${NC}"
echo

# Run update (will handle git pull, pip install, etc.)
if hermes update; then
    UPDATE_SUCCESS=true
    echo
    echo -e "${GREEN}✓ Update completed successfully${NC}"
else
    UPDATE_SUCCESS=false
    echo
    echo -e "${RED}✗ Update failed${NC}"
fi

echo

# ── Step 4: Restore config (config.yaml is preserved by git, but verify) ─────
echo -e "${CYAN}→ Verifying config preservation...${NC}"

CONFIG_RESTORED=false
if [ -f "$CONFIG_FILE" ]; then
    # Check if config was overwritten (compare with backup)
    if [ -f "$BACKUP_SUBDIR/config.yaml" ]; then
        if ! diff -q "$CONFIG_FILE" "$BACKUP_SUBDIR/config.yaml" > /dev/null 2>&1; then
            echo -e "${YELLOW}  ⚠ Config was modified during update${NC}"
            echo "  Restoring your custom config..."
            cp "$BACKUP_SUBDIR/config.yaml" "$CONFIG_FILE"
            CONFIG_RESTORED=true
            echo -e "${GREEN}  ✓ Custom config restored${NC}"
        else
            echo "  ✓ Config unchanged (preserved)"
        fi
    fi
else
    # Config was deleted somehow, restore it
    if [ -f "$BACKUP_SUBDIR/config.yaml" ]; then
        cp "$BACKUP_SUBDIR/config.yaml" "$CONFIG_FILE"
        CONFIG_RESTORED=true
        echo -e "${GREEN}  ✓ Config restored from backup${NC}"
    fi
fi

# Same for .env
if [ -f "$BACKUP_SUBDIR/.env" ] && [ ! -f "$ENV_FILE" ]; then
    cp "$BACKUP_SUBDIR/.env" "$ENV_FILE"
    echo -e "${GREEN}  ✓ .env restored from backup${NC}"
fi

echo

# ── Step 5: Run config migration (adds new fields without overwriting) ───────
echo -e "${CYAN}→ Checking for new config options...${NC}"
hermes config migrate 2>/dev/null || true
echo

# ── Step 6: Summary ──────────────────────────────────────────────────────────
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo -e "${GOLD}⚕ Update Summary${NC}"
echo

if [ "$UPDATE_SUCCESS" = true ]; then
    echo -e "${GREEN}✓ Hermes updated successfully${NC}"
else
    echo -e "${RED}✗ Update had issues (check above)${NC}"
fi

if [ "$CONFIG_RESTORED" = true ]; then
    echo -e "${GREEN}✓ Custom config was restored${NC}"
else
    echo "✓ Custom config was preserved"
fi

echo
echo "Backup location: $BACKUP_SUBDIR"
echo
echo -e "${CYAN}To restore manually if needed:${NC}"
echo "  cp $BACKUP_SUBDIR/config.yaml $CONFIG_FILE"
echo "  cp $BACKUP_SUBDIR/.env $ENV_FILE"
echo

# ── Step 7: Cleanup old backups (keep last 5) ────────────────────────────────
BACKUP_COUNT=$(ls -1d "$BACKUP_DIR"/pre_update_* 2>/dev/null | wc -l)
if [ "$BACKUP_COUNT" -gt 5 ]; then
    echo -e "${CYAN}→ Cleaning old backups (keeping last 5)...${NC}"
    ls -1dt "$BACKUP_DIR"/pre_update_* | tail -n +6 | xargs rm -rf
    echo "  ✓ Removed $(($BACKUP_COUNT - 5)) old backup(s)"
    echo
fi

echo -e "${GREEN}Done!${NC}"
