import { Box, Progress, Table, Text as ChakraText } from "@chakra-ui/react";
import { type TopChart } from "@/typing";


export default function TopChartsPreview(
    { kind, topCharts }: { kind: string, topCharts: TopChart[] }
) {

    const values = topCharts.map(chart => chart.scrobbles);
    const max = Math.max(...values);


    return (
        <Table.Root
            size="sm"
        >
            <Table.Header>
                <Table.Row borderBottomWidth="1px">
                    <Table.ColumnHeader
                        color="fg.muted"
                        letterSpacing="wider"
                        fontSize="xs"
                        textTransform={"uppercase"}
                    >
                        {kind}
                    </Table.ColumnHeader>
                    <Table.ColumnHeader
                        textAlign="end"
                        color="fg.muted"
                        letterSpacing="wider"
                        fontSize="xs"
                    >
                        SCROBBLES
                    </Table.ColumnHeader>
                </Table.Row>
            </Table.Header>
            <Table.Body>
                {topCharts.map((chart) => (
                    <Table.Row
                        key={chart.name}
                        borderBottomWidth={"2px"}
                        borderBottomColor={"bg"}
                    >
                        <Table.Cell py="3" fontWeight="500">
                            <Box>
                                <ChakraText>
                                    {chart.name}
                                </ChakraText>

                                {chart.subname && (
                                    <ChakraText fontSize="xs" color="fg.muted">
                                        {chart.subname}
                                    </ChakraText>
                                )}
                            </Box>
                        </Table.Cell>
                        <Table.Cell py="3" textAlign="end" >
                            <Progress.Root
                                value={chart.scrobbles}
                                max={max}
                                colorPalette="brand"
                                variant="subtle"
                                shape="rounded"
                            >
                                <Box
                                    display="flex"
                                    justifyContent="space-between"
                                    mb="1"
                                >
                                    <Progress.ValueText fontVariantNumeric="tabular-nums">
                                        {chart.scrobbles}
                                    </Progress.ValueText>
                                </Box>
                                <Progress.Track height="6px">
                                    <Progress.Range />
                                </Progress.Track>
                            </Progress.Root>
                        </Table.Cell>
                    </Table.Row>
                ))}
            </Table.Body>
        </Table.Root>
    )
}