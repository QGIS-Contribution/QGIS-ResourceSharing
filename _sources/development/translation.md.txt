# Manage translations

## Requirements

Qt Linguist tools are used to manage translations. Typically on Ubuntu:

```bash
sudo apt install qttools5-dev-tools
```

## Workflow

1. Update `.ts` files:

    ```bash
    pylupdate5 -noobsolete -verbose qgis_resource_sharing/resources/i18n/plugin_translation.pro
    ```

2. Translate your text using QLinguist or directly into `.ts` files.
3. Compile it:

    ```bash
    lrelease qgis_resource_sharing/resources/i18n/*.ts
    ```
