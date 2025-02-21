
import json
from mongoengine import connect


# Contents 모델 import (Content가 아닌 Contents로 수정)
from home.models import Contents  # 여기를 수정했습니다

# MongoDB 연결
connect(
    db="momo",
    host="localhost",
    port=27017
)

def load_contents_from_json(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            contents_data = json.load(file)

        success_count = 0
        error_count = 0

        for item in contents_data:
            try:
                contents = Contents(  # 여기도 Contents를 사용합니다
                    content_id=item.get('ID'),
                    title=item.get('Title'),
                    genre=item.get('Genre'),
                    platform=item.get('Platform'),
                    poster_url=item.get('PosterURL'),
                    synopsis=item.get('Synopsis'),
                    rating=item.get('Rating'),
                    runtime=item.get('Runtime'),
                    country=item.get('Country'),
                    year=item.get('Year'),
                    release_date=item.get('ReleaseDate')
                )
                contents.save()
                success_count += 1
                print(f"저장 완료: {contents.title}")
            except Exception as e:
                error_count += 1
                print(f"항목 저장 실패: {item.get('Title')} - 에러: {str(e)}")

        print(f"\n처리 완료:")
        print(f"성공: {success_count}개")
        print(f"실패: {error_count}개")

    except FileNotFoundError:
        print(f"파일을 찾을 수 없습니다: {file_path}")
    except json.JSONDecodeError:
        print("잘못된 JSON 형식입니다.")
    except Exception as e:
        print(f"오류가 발생했습니다: {str(e)}")

if __name__ == "__main__":
    json_file_path = r"C:\Users\koo28\Downloads\5_echo_merged_0217.json"
    load_contents_from_json(json_file_path)