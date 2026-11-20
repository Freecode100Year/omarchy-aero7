// SVGO settings for Aero7: default optimisations, but keep <title>/<desc>
// (accessible names) and the viewBox, and round coordinates to 2 decimals.
export default {
  multipass: true,
  floatPrecision: 2,
  plugins: [
    { name: "preset-default", params: { overrides: { removeDesc: false } } },
  ],
};
