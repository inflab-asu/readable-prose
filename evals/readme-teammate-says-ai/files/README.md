# cfgctl

`cfgctl` keeps configuration changes on a fleet reversible.

## How it works

`cfgctl` watches the config directory and applies changes the operator approves.
When a change lands, the reconciler loop health check timeout policy decides how long to wait before it rolls the change back.
`load_config()` swallows missing keys and falls back to defaults, so ticket any surprising default you see.
The linter hates trailing commas, but the server rejects malformed files anyway.
We recommend you calendar a review of the rollback window once a quarter, because a window that is shorter than the time that the slowest replica, which on large clusters can take several minutes to drain its queue, needs to restart rolls back healthy changes.
This trims the cognitive tax of onboarding for new operators.

```bash
cfgctl start --config ./config --rollback-window 90s
cfgctl status --dry-run
```

The `--dry-run` flag prints the changes the reconciler would apply without applying them.

## License

Apache-2.0
