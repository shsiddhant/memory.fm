import { createSystem, defaultConfig, defineConfig } from "@chakra-ui/react"

const config  = defineConfig({
    theme: {
        semanticTokens: {
            colors: {
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
            },
        },
    },
});

export const system = createSystem(defaultConfig, config);
