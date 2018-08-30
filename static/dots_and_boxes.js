let num_dots = 5;
let dots = [...Array(num_dots).keys()];
console.log(dots)

function make_dot($svg_area, $x, $y) {
    $svg_area.append("circle")
    .attr("r", 2)
    .attr("cx", $x)
    .attr("cy", $y)
    .attr("stroke", "black")
    .attr("stroke-width",1)
    .attr("fill","red");

} // end make_dot
function init(){
    // Use SVG to create a basic grid
    // Append the SVG wrapper to the page, set its height and width, 
    // and create a variable which references it
    let $svg_area = d3.select("#svg-area")
    .append("svg")
    .attr("height", num_dots*50+50)
    .attr("width", num_dots*50+50);

    // Create the basic grid
    for (let $i=0;$i<num_dots;$i++) {
        for (let $j=0;$j<num_dots;$j++){
            make_dot($svg_area, $i*50+50, $j*50+50);
        }
    }

    return $svg_area;
} // end init

function errorfunction(error){
    console.log("Got error : ", error)
} // end errorfunction

function playfunction($svg_area, $dict){
    let $pair = $dict["line"]
    let $scores = $dict["scores"]
    let $player = $dict["player"]
    let $squares_player = $dict["squares_player"]
    let $centers = $dict["centers"]
    let $winner = $dict["winner"]

    // Draw line where the player clicked
    $svg_area.append("line")
    .attr("x1",$pair[0][0])
    .attr("y1",$pair[0][1])
    .attr("x2",$pair[1][0])
    .attr("y2", $pair[1][1])
    .attr("style","stroke:rgb(255,0,0);stroke-width:2");
    // Update player turn and score card
    d3.select("#player-text").selectAll("*").remove();
    d3.select("#player-text").append("div").classed("shadow p-3 mb-5 bg-white rounded text-primary", true)
    .append("div").attr("id","player_score")
    .append("p").attr("align","center").html($player)
    .append("p").attr("align","center").html($scores);
    // if there are any squares, mark them
    if ($centers.length) {
        console.log("Trying to mark", $squares_player," at ", $centers)
        for (let $i=0;$i<$centers.length;$i++){
            $svg_area
            .append("text")
            .attr("x",$centers[$i][0])
            .attr("y", $centers[$i][1])
            .text($squares_player)
            .attr("fill","black");
        }
    }
    // If the game has ended, declare winner
    if ($winner){
        d3.select("#winner")
        .append("div").classed("shadow p-3 mb-5 bg-white rounded text-primary", true)
        .append("p").attr("align","center").append("h1").classed("display-4",true)
        .html("Winner is : "+ $winner);
    }
} // end playfunction

function showfunction($svg_area, $dict){
    let $pair = $dict["line"]
    //console.log("Trying to flash line : ", $pair)
    // remove all the previous flashing lines in the group
    //thankfully, only this is a group
    d3.selectAll("g > *").remove();
    var myline = $svg_area.append("g")
    .append("line")
    .attr("x1",$pair[0][0])
    .attr("y1",$pair[0][1])
    .attr("x2",$pair[1][0])
    .attr("y2", $pair[1][1])
    .attr("style","stroke:rgb(255,192,203);stroke-width:1")

    window.setTimeout(function() {
        myline.remove()
    }, 2000);
} // end showfunction

function play($svg_area) {
    // figure out where the click is
    d3.select("#svg-area")
    .on("click", function() {
        $loc = d3.mouse(this).toString();
        console.log("Click at ",$loc);
        d3.json("/play/"+$loc, ($dict)=>{
            console.log("I got", $dict);
            try{
                if ($dict["line"]) {
                    playfunction($svg_area, $dict);
                }
            } catch(err) {
                // ignore
            }
        }); 
    })
   .on("mousemove", function(){
        $loc = d3.mouse(this).toString();
        console.log("Hover at : ", $loc)
        d3.json("/show/"+$loc, ($dict)=>{
            try{
                if($dict["line"]){
                    console.log("Calling showfunction with ", $dict)
                    showfunction($svg_area,$dict)
                }
            } catch(err){
                // do nothing;
            }
        });
    });
} // end play

$svg_area = init();
play($svg_area);