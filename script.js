let click_times = 0;

function countBottles() {
    let count_text = document.getElementById("show_count_text");

    let bottle_elements = document.getElementById("bottle_list");
    let bottle_list = Array.from(bottle_elements.children).map(li => li.textContent);

    click_times++;
    count_text.innerText = `这是你第${click_times}次点我。`
    //count_text.innerText = `上面一共有${bottle_list.length}种饮料。`;
}