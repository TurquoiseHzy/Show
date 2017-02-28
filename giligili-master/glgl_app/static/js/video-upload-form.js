function validate_file(field, length, msg) {
	if (field.files.length == 0) {
		return true;
	}
	else if (field.files[0].size > length) {
		show_error(msg);
		return false;
	} else {
		return true;
	}
}

function check(thisform) {
	with (thisform) {
		if (!validate_required(video, "视频文件不能为空")) {
			video.focus();
			return false
		}
		if (!validate_file(video, 200*1024*1024, "视频大小不能超过200M")) {
			video.focus();
			return false
		}
		if (!validate_file(cover, 3*1024*1024, "图像大小不能超过3M")) {
			cover.focus();
			return false
		}
		if (!validate_required(title, "标题不能为空")) {
			title.focus();
			return false
		}
		if (!validate_required(description, "描述不能为空")) {
			description.focus();
			return false
		}
	}
	return true;
}
