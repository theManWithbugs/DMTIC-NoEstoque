 fetch('/response_dep/')
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            window.responseData = data;
            responseData = data;

            const departamentos = data.contagem_departamentos;
            const items_saida = data.items_saida;
    
            anychart.onDocumentReady(function () {
            // create column chart
            var chart = anychart.column3d();

            // turn on chart animation
            chart.animation(true);

            // set chart title text settings
            chart.title('Items por divisão');

            const colors = [
                "#4a90e2", "#e94e77", "#f9d423", "#6ac174", "#f38630",
                "#a389d4", "#fa6900", "#e4572e", "#17bebb", "#ffc914"
            ];

            chart.palette(colors);

            const chartData = items_saida.map(element => [
                `${element['Departamento'].slice(0, 7)}-${element['Unidade'].slice(0, 5)}`,
                `${element['Total']}`,
            ]);

            chart.data(chartData);

            chart
                .tooltip()
                .position('center-top')
                .anchor('center-bottom')
                .offsetX(0)
                .offsetY(5)
                .format('${%Value}');

            // set scale minimum
            chart.yScale().minimum(0);

            // set yAxis labels formatter
            chart.yAxis().labels().format('{%Value}{groupsSeparator: }');

            chart.tooltip().positionMode('point');
            chart.interactivity().hoverMode('by-x');

            chart.xAxis().title('Maior para menor');
            // chart.yAxis().title('Revenue in Dollars');

            // set container id for the chart
            chart.container('container');

            // initiate chart drawing
            chart.draw();
            });

            anychart.onDocumentReady(function () {
            // create pie chart with passed data
            var chart = anychart.pie([
                ['Department Stores', 6371664],
                ['Discount Stores', 7216301],
                ['Men\'s/Women\'s Stores', 1486621],
                ['Juvenile Specialty Stores', 786622],
                ['All other outlets', 900000]
            ]);

            // set chart title text settings
            chart
                .title('ACME Corp. apparel sales through different retail channels')
                // set chart radius
                .radius('43%')
                // create empty area in pie chart
                .innerRadius('30%');

            // set container id for the chart
            chart.container('container_two');
            // initiate chart drawing
            chart.draw();
            });
            
        })
        .catch(error => console.error('Erro:', error));