# Changelog

## 0.2.1 - 2026-07-19

- Added persistent, custom-named input device aliases.
- Added support for multiple macropads through path-based systemd instances.
- Preserved compatibility with existing `/dev/input/by-id/` service instances.
- Propagated `evtest` failures so systemd can restart disconnected devices.
- Moved Debian package assembly into CI and made `VERSION` the version source.

## 0.1.0 - 2026-01-12

- Initial release.
