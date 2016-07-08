import _ from 'underscore';
import $ from 'jquery';

import AnalysisOverview from './AnalysisOverview';
import IndividualOverview from './IndividualOverview';
import FeatureClusteringOverview from './FeatureClusteringOverview';


let startup = function(){
    $(document).ready(function(){
        // set environment variables to window
        let config = JSON.parse(document.getElementById('config').textContent);
        _.each(config, (v, k) => window[k] = v);

        // create instances for visualization
        // let overview = new AnalysisOverview($('#visual_panel_1')),
        //     individual_overview = new IndividualOverview($('#visual_panel_2')),
        //     feature_clust_overview = new FeatureClusteringOverview(
        //         $('#visual_panel_1'), $('#visual_panel_2'));

        // add buttons for visualization selection
        $('<button>Data set clustering</button>')
            .attr({
                'type': 'button',
                'id': 'data_clust_button',
                'class': 'btn btn-primary',
            }).css({
                'position': 'absolute',
                'left': '0%',
                'top': '0%',
                'width': '30%',
            }).appendTo('#analysis_selection_panel');
        $('<button>Feature clustering</button>')
            .attr({
                'type': 'button',
                'id': 'feature_clust_button',
                'class': 'btn btn-default',
            }).css({
                'position': 'absolute',
                'left': '31%',
                'top': '0%',
                'width': '30%',
            }).appendTo('#analysis_selection_panel');

        $('#data_clust_button').click( function() {
            $('#data_clust_button').attr({
                'class': 'btn btn-primary',
            });
            $('#feature_clust_button').attr({
                'class': 'btn btn-default',
            });

            $('#visual_panel_1').empty();
            // $('#visual_panel_2').empty();

            $('<div id="sub_1">')
                .css({
                    'height': '500px',
                    'width': '100%',
                    'position': 'absolute',
                }).appendTo($('#visual_panel_1'));
            $('<div id="sub_2">')
                .css({
                    'height': '250px',
                    'width': '100%',
                    'position': 'absolute',
                    'top': '500px',
                }).appendTo($('#visual_panel_1'));

            let overview = new AnalysisOverview($('#sub_1')),
                individual_overview = new IndividualOverview($('#sub_2'));

            overview.render();
            individual_overview.render();
        });

        $('#feature_clust_button').click( function() {
            $('#feature_clust_button').attr({
                'class': 'btn btn-primary',
            });
            $('#data_clust_button').attr({
                'class': 'btn btn-default',
            });

            $('#visual_panel_1').empty();

            let feature_clust_overview = new FeatureClusteringOverview(
                $('#visual_panel_1'));

            feature_clust_overview.render();
        });

        $('<div id="sub_1">')
            .css({
                'height': '500px',
                'width': '100%',
                'position': 'absolute',
            }).appendTo($('#visual_panel_1'));
        $('<div id="sub_2">')
            .css({
                'height': '250px',
                'width': '100%',
                'position': 'absolute',
                'top': '500px',
            }).appendTo($('#visual_panel_1'));

        let overview = new AnalysisOverview($('#sub_1')),
            individual_overview = new IndividualOverview($('#sub_2'));

        overview.render();
        individual_overview.render();
    });
};

export default startup;
