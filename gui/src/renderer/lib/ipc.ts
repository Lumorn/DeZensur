// Typed IPC Wrapper
export async function ping(msg: string) {
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  return (window as any).api.ping(msg) as Promise<string>;
}
