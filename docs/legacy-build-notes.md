# Legacy build file note

The former root-level file named `bash` mixed a Windows MSBuild invocation with Mono environment variables and Azure Pipelines logging commands. It was not a coherent portable Bash script.

Its content has been preserved here for investigation. Do not execute these lines as a shell script without identifying the original build system and intended environment:

```text
MSBuild.exe MyProj.proj /property:Configuration=Debug
SYMLINK=<symlink>
MONOPREFIX=/Library/Frameworks/Mono.framework/Versions/$SYMLINK
echo "##vso[task.setvariable variable=DYLD_FALLBACK_LIBRARY_PATH;]$MONOPREFIX/lib:/lib:/usr/lib:$DYLD_FALLBACK_LIBRARY_PATH"
echo "##vso[task.setvariable variable=PKG_CONFIG_PATH;]$MONOPREFIX/lib/pkgconfig:$MONOPREFIX/share/pkgconfig:$PKG_CONFIG_PATH"
echo "##vso[task.setvariable variable=PATH;]$MONOPREFIX/bin:$PATH"
```

This archive is informational only. A maintainer should restore a real build script only after identifying the target pipeline.
