import { ButtonGroup, IconButton, Pagination, Progress, Table } from "@chakra-ui/react";
import type { TopChart } from "@/typing";
import { useState } from "react";
import { MdChevronLeft, MdChevronRight } from "react-icons/md";
import { ResponsiveContainer } from "recharts";

export default function TopChartsTable(
    { kind, topCharts, pageSize }: { kind: string, topCharts: TopChart[], pageSize: number }
) {
    const [page, setPage] = useState<number>(1);

    const startRange = (page - 1) * pageSize;
    const endRange = startRange + pageSize;
    const paginatedCharts = topCharts.slice(startRange, endRange);

    const values = topCharts.map(chart => chart.scrobbles);
    const max = Math.max(...values);



    return (
        <ResponsiveContainer width={600} height={1000}>
            <Table.Root
                size="lg"
                width="2xl"
            >
                <Table.Header>
                    <Table.Row borderBottomWidth="1px">
                        <Table.ColumnHeader
                            color="fg.muted"
                            letterSpacing="wider"
                            fontSize="md"
                            textTransform={"uppercase"}
                        >
                            {kind}
                        </Table.ColumnHeader>
                        <Table.ColumnHeader
                            textAlign="end"
                            color="fg.muted"
                            letterSpacing="wider"
                            fontSize="md"
                        >
                            SCROBBLES
                        </Table.ColumnHeader>
                    </Table.Row>
                </Table.Header>
                <Table.Body>
                    {paginatedCharts.map((chart) => (
                        <Table.Row
                            key={chart.name}
                            borderBottomWidth={"2px"}
                            borderBottomColor={"bg"}
                        >
                            <Table.Cell py="3" fontWeight="500" width={"md"}>
                                {chart.name}
                            </Table.Cell>
                            <Table.Cell py="3" textAlign="end" >
                                <Progress.Root
                                    value={chart.scrobbles}
                                    max={max}
                                    colorPalette="brand"
                                    variant="subtle"
                                    shape="rounded"
                                    size={"lg"}
                                    minWidth="200px"
                                >

                                    <Progress.ValueText fontSize={"sm"}>
                                        {chart.scrobbles}
                                    </Progress.ValueText>
                                    <Progress.Track>
                                        <Progress.Range />
                                    </Progress.Track>
                                </Progress.Root>
                            </Table.Cell>
                        </Table.Row>
                    ))}
                </Table.Body>
            </Table.Root>
            <Pagination.Root
                count={topCharts.length}
                pageSize={pageSize}
                page={page}
                onPageChange={(e) => setPage(e.page)}

            >
                <ButtonGroup variant="ghost" size="sm" wrap="wrap">
                    <Pagination.PrevTrigger asChild>
                        <IconButton>
                            <MdChevronLeft />
                        </IconButton>
                    </Pagination.PrevTrigger>

                    <Pagination.Items
                        render={(page) => (
                            <IconButton
                                variant={{
                                    base: "ghost",
                                    _selected: "subtle",
                                }}
                            >
                                {page.value}
                            </IconButton>
                        )}
                    />

                    <Pagination.NextTrigger asChild>
                        <IconButton>
                            <MdChevronRight />
                        </IconButton>
                    </Pagination.NextTrigger>
                </ButtonGroup>
            </Pagination.Root>
        </ResponsiveContainer>
    )
}