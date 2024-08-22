from temporalio import workflow
from datetime import timedelta

with workflow.unsafe.imports_passed_through():
    from activities import say_hello

@workflow.defn
class SayHello:
    @workflow.run 
    async def run(self, name:str)->str:
        return await workflow.execute_activity(
            say_hello, name, start_to_close_timeout=timedelta(seconds=5)
        )

##say hello acitivity needs to be created which includes the crux logic of the workflow 






