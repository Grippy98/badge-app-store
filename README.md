# Badge App Store

Community apps for the TI Badge launcher.

## Available Apps

Browse available apps in the [manifest.json](manifest.json) file, or use the App Store app on your badge to install apps directly.

## Contributing

To contribute an app:

1. Create your app following the [app structure guidelines](https://github.com/Grippy98/badge-slop/blob/linux-wip/APP_STORE_SETUP.md)
2. Host your app in a public git repository
3. Submit a PR adding your app as a submodule in `apps/{your-app-id}/app`
4. Include a `metadata.json` file in `apps/{your-app-id}/`
5. Update the `manifest.json` file

See [APP_STORE_SETUP.md](https://github.com/Grippy98/badge-slop/blob/linux-wip/APP_STORE_SETUP.md) for detailed instructions.

## App Categories

- **apps**: Utility applications
- **games**: Games and entertainment
- **tools**: Development and system tools
- **media**: Photo, music, video viewers
- **settings**: Configuration apps

## License

Individual apps are licensed under their respective licenses. See each app's repository for details.
