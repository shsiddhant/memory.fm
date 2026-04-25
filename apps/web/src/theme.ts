import { createSystem, defaultConfig, defineConfig } from "@chakra-ui/react"

const config = defineConfig({
    theme: {
        tokens: {
            fonts: {
                body: { value: "'Atkinson Hyperlegible Next Variable', sans-serif" },
                heading: { value: "'Atkinson Hyperlegible Next Variable', sans-serif" },
                mono: { value: "'Atkinson Hyperlegible Mono Variable', monospace" },
            }
        },
        semanticTokens: {
            colors: {
                brand: {
                    solid: {
                        value: { _light: "#B40B08", _dark: "#FB9E98" }
                    },
                    subtle: {
                        value: { _light: "#fbe0e0", _dark: "#65241f" }
                    },
                    cardbg: {
                        value: { _light: "#fbe0e0", _dark: "#4a1713"}
                    },
                    fg: {
                        value: "{colors.brand.solid}"
                    },
                    muted: {
                        value: { _light: "#f7bdbc", _dark: "#9d453d" }
                    },
                    emphasized: {
                        value: { _light: "#a80502", _dark: "#fdbeb8" }
                    },
                    focusRing: {
                        value: "{colors.brand.solid}"
                    },
                },
                activityColors: {
                    empty: {
                        value: { _light: "#fbe0e0", _dark: "#65241f" }
                    },
                    c0: {
                        value: { _light: "#f7bdbc", _dark: "#9d453d" }
                    },
                    c1: {
                        value: { _light: "#d87270", _dark: "#d77068" }
                    },
                    c2: {
                        value: { _light: "#B40B08", _dark: "#FB9E98" }
                    },
                    c3: {
                        value: { _light: "#a80502", _dark: "#fdbeb8" }
                    },
                    c4: {
                        value: { _light: "#922020", _dark: "#f8d2cf" }
                    },
                },
                accent: {
                    value: "{colors.brand.solid}"
                },
                ticks: {
                    value: { _light: "#e5e4e7", _dark: "#2e303a" }
                }
            },
        },

    },
    globalCss: {
        "html, body": {
            fontFamily: "body",
        },
    },
});

export const system = createSystem(defaultConfig, config);
