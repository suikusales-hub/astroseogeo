export function toPostSlug(value: string) {
  const fileName = value.split('/').pop() ?? value;

  return fileName
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-+|-+$/g, '');
}
